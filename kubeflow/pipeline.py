from kfp import dsl

@dsl.pipeline(name="rag-nl-refresh")
def rag_nl_refresh_pipeline():
    # Replace with container components for fetch -> chunk -> embed -> index.
    pass
