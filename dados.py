import pandas as pd
BASE = "base/desafio_tecnico_ai_eng - {}.csv"

produtos = pd.read_csv(BASE.format("products")).merge(
    pd.read_csv(BASE.format("categories"))[["category_id","name"]]
      .rename(columns={"name":"categoria"}), on="category_id")

promo = pd.read_csv(BASE.format("promotions"))
promo = promo[promo.is_active == 1].groupby("product_id", as_index=False)["discount_percent"].max()
produtos = produtos.merge(promo, on="product_id", how="left")
produtos["preco_final"] = produtos.price_brl * (1 - produtos.discount_percent.fillna(0)/100)