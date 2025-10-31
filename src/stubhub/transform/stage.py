import polars as pl
from prefect import task

from stubhub.transform.models import Items


@task(name="JSON to DF")
def json_to_df(
    responses: list[dict], stubhub_name: str, stubhub_id: int
) -> pl.DataFrame:
    """
    Converts incoming responses to df
    """
    items = Items.model_validate(
        [response.get("items")[0] for response in responses if response.get("items")]
    )

    return items.to_df().with_columns(
        pl.lit(stubhub_name).alias("stubhub_name"),
        pl.lit(stubhub_id).alias("stubhub_id"),
    )
