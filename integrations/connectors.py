import csv
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

@dataclass(frozen=True)
class Source:
    id: str
    kind: str
    location: str

class Registry:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.sources = {}
        self.health = {}
    def register(self, source):
        if not source.id or source.id in self.sources:
            raise ValueError('missing or duplicate source ID')
        if source.kind not in {'csv','excel','json','accounting','crm','accounting_http','crm_http'}:
            raise ValueError('unsupported connector')
        self.sources[source.id] = source
        self.health[source.id] = {'status':'unchecked'}
    def read(self, source_id):
        source = self.sources[source_id]
        try:
            rows = self._read(source)
            if not isinstance(rows,list) or any(not isinstance(r,dict) for r in rows):
                raise ValueError('expected list of records')
        except Exception as exc:
            self.health[source_id] = {'status':'failed','error_type':type(exc).__name__,'checked_at':datetime.now(timezone.utc).isoformat()}
            raise
        self.health[source_id] = {'status':'healthy','rows':len(rows),'checked_at':datetime.now(timezone.utc).isoformat()}
        return rows
    def _read(self, source):
        if source.kind in {'accounting_http','crm_http'}:
            from integrations.mock_http import fetch
            return fetch(int(source.location), source.kind.removesuffix('_http'))
        path = (self.root / source.location).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError('path outside fixture root')
        if source.kind == 'csv':
            with path.open(newline='',encoding='utf-8-sig') as f:
                reader=csv.DictReader(f)
                if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames): raise ValueError('invalid headers')
                rows=list(reader)
                if any(None in r or None in r.values() for r in rows): raise ValueError('invalid CSV row width')
                return rows
        if source.kind == 'excel':
            from openpyxl import load_workbook
            wb=load_workbook(path,read_only=True,data_only=True)
            try:
                it=wb.active.values
                headers=next(it,())
                if not headers or any(not isinstance(h,str) or not h.strip() for h in headers) or len(set(headers))!=len(headers): raise ValueError('invalid headers')
                return [dict(zip(headers,row)) for row in it if any(v is not None for v in row)]
            finally: wb.close()
        with path.open(encoding='utf-8') as f: payload=json.load(f)
        if source.kind in {'accounting','crm'}:
            if not isinstance(payload,dict) or payload.get('simulated') is not True: raise ValueError('simulation fixture required')
            return payload['records']
        return payload
