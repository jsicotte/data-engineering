import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import polars as pl
    from datetime import date
    return date, pl


@app.cell
def _(date, pl):
    example_df = pl.DataFrame(
        {
            "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
            "birthdate": [
                date(1997, 1, 10),
                date(1985, 2, 15),
                date(1983, 3, 22),
                date(1981, 4, 30),
            ],
            "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
            "height": [1.56, 1.77, 1.65, 1.75],  # (m)
        }
    )
    example_df
    return (example_df,)


@app.cell
def _(example_df):
    example_df.glimpse()
    return


@app.cell
def _(example_df):
    example_df.schema
    return


if __name__ == "__main__":
    app.run()
