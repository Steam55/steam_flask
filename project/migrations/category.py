from ..models import Category
from .. import db
from ..utils import create_slug

data_category = [
    {
        "name": "Populaires",
        "icon": "food/category/burger.png"
    },
    {
        "name": "Pâtes",
        "icon": "food/category/assiette.png"
    },
    {
        "name": "Riz",
        "icon": "food/category/riz.png"
    },
    {
        "name": "Spaghettis",
        "icon": "food/category/plat-de-spaghettis.png"
    },
    {
        "name": "Tchatchaga",
        "icon": "food/category/boule-de-viande.png"
    },
    {
        "name": "Cocktail",
        "icon": "food/category/cocktail-avec-tranche-de-citron.png"
    },
    {
        "name": "Viande",
        "icon": "food/category/porc.png"
    },
    {
        "name": "Piron",
        "icon": "food/category/nourriture.png"
    },
    {
        "name": "Shawarma",
        "icon": "food/category/boule-de-viande.png"
    },
    {
        "name": "Pizza",
        "icon": "food/category/pizza.png"
    },
    {
        "name": "Hamburger",
        "icon": "food/category/burger.png"
    },
    {
        "name": "Salade",
        "icon": "food/category/nourriture-et-restaurant.png"
    },
]

class CategoryMigration:
    @classmethod
    def migrate(cls):
        for item in data_category:
            slug = create_slug()
            category = Category(
                item.get("name"), 
                item.get("icon"), 
                "category-" + slug
                )
            db.session.add(category)
            db.session.commit()
