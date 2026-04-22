import typer
from src.cli.commands import (
    get_seller_info, get_warehouses, get_inventory, 
    get_products, get_media, set_price,
    get_users, general_extra, products_extra
)

app = typer.Typer(help="Wildberries CLI Utility")

# Регистрируем команды
app.command(name="get-seller-info")(get_seller_info.get_seller_info)
app.command(name="get-warehouses")(get_warehouses.get_warehouses)
app.command(name="get-inventory")(get_inventory.get_inventory)
app.command(name="get-products")(get_products.get_products)
app.command(name="products-get-brands")(products_extra.get_brands)
app.command(name="products-get-subjects")(products_extra.get_subjects)
app.command(name="get-media")(get_media.get_media)
app.command(name="set-price")(set_price.set_price)
app.command(name="get-users")(get_users.get_users)
app.command(name="get-news")(general_extra.get_news)
app.command(name="get-rating")(general_extra.get_rating)
app.command(name="ping")(general_extra.ping)

if __name__ == "__main__":
    app()
