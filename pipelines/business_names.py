"""Fictional directory, stable across runs; no transaction RNG consumed."""
from itertools import product
import random
# Distinct coined trading identities, with varied sector descriptors and legal styles.
first="Alder Amber Ash Avon Birch Bracken Bronze Cairn Cedar Claret Clover Copper Coral Crest Dapple Dawn Drift Elm Ember Fern Flint Fox Frost Glen Granite Hazel Heather Heron Holly Indigo Iris Juniper Kestrel Larch Laurel Linden Maple Marlin Meadow Moss Oak Onyx Orchard Otter Pearl Pine Quartz Raven Reed Rowan Sable Sage Silver Slate Sorrel Spruce Stone Swift Thistle Vale Willow Wren Yew".split()
second="arc bank bay beck bend bridge brook burn coast court cove crest dale dell den edge field ford forge gate glade grove harbour haven heath hill hollow isle lane lea ledge light lock marsh mere mill moor mount park path point ridge rise rock shore spring stead strand stream vale view walk ward water way well wick wood yard".split()
sectors=["Construction","Civil Works","Building & Renovation","Groundworks","Roofing","Electrical Services","Plumbing & Heating","Fitouts","Property Projects","Joinery","Landscape Design","Contracting","Building Maintenance","Engineering","Interiors","Masonry","Development","Trade Centre","Builders Merchants","Mechanical Services","Homes","Restoration","Site Services","Flooring","Steelwork","Drylining","Facilities","Paving","Scaffolding","Energy Retrofit","Design & Build","Carpentry"]
supply=["Aggregates","Timber & Panels","Insulation Systems","Fixings","Roofing Products","Paint & Coatings","Industrial Distribution","Pipe & Valve","Electrical Wholesale","Cement Products","Safety Equipment","Building Chemicals","Trade Imports","Metal Fabrication","Tool Supply","Masonry Products","Drainage Systems","Hardware","Materials Logistics","Glass & Glazing","Adhesives","Cladding","Flooring Supply","Ventilation"]
rng=random.Random(8261)
identities=[a+b for a,b in product(first,second) if a.lower()!=b]
rng.shuffle(identities)
def names(stems,types):
    out=[]
    for i,stem in enumerate(stems):
        sector=types[i%len(types)]
        style=i%7
        out.append([f"{stem} {sector}",f"{stem} {sector} Ltd",f"{stem} & Co. {sector}",f"{stem} Group",f"{stem} {sector} Ireland",f"{stem} {sector} Partners",f"{stem} {sector} Solutions"][style])
    return out
CUSTOMERS=names(identities[:500],sectors)
SUPPLIERS=names(identities[500:600],supply)
assert len(set(CUSTOMERS+SUPPLIERS))==600
