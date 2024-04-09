# How-To: Use Similarity Indexes with Data from Custom Sources

[The similarity index](../concepts/similarity_indexes.md) is a feature provided by db-ally, designed to map a user input to the nearest matching value in the data source, using a chosen similarity metric. In this guide, we'll show you how to set up a similarity index to use data from a custom source.

## Understanding How a Similarity Index Works

A similarity index is composed of two main parts:

* A **fetcher** that collects all possible values from a data source
* A **store** that indexes these values, allowing the system to find the nearest match to the user's input

To use a similarity index with data from a custom source, you need to create a customized fetcher that retrieves the data from your source.

## Creating a Custom Fetcher

To craft a custom fetcher, you need to create a class extending the `AbstractFetcher` class provided by db-ally. The `AbstractFetcher` class possesses a single asynchronous method, `fetch`, which you need to implement. This method should give back a list of strings representing all possible values from your data source.

For example, if you wish to index the list of dog breeds from the web API provided by [dog.ceo](https://dog.ceo/), you can create a fetcher like this:

```python
from dbally.similarity.fetcher import AbstractFetcher
import requests

class DogBreedsFetcher(AbstractFetcher):
    async def fetch(self):
        response = requests.get('https://dog.ceo/api/breeds/list/all').json()
        breeds = response['message'].keys()
        return list(breeds)
```

In this example, the `DogBreedsFetcher` class fetches the list of dog breeds from the dog.ceo API and gives it back as a list of strings. You can then employ this fetcher to establish a similarity index that maps user input to the most similar dog breed.

## Using the Custom Fetcher with a Similarity Index

Upon implementing your custom fetcher, you can use it to set up a similarity index. Here's an example demonstrating how to generate a similarity index using the `DogBreedsFetcher` class:

```python
from dbally.similarity.index import SimilarityIndex
from dbally.similarity.store import FaissStore

breeds_similarity = SimilarityIndex(
    fetcher=DogBreedsFetcher(),
    store=FaissStore(
    index_dir="./similarity_indexes",
    index_name="breeds_similarity",
    embedding_client=OpenAiEmbeddingClient(
        api_key="your-api-key",
    )
)
```

In this example, we used the FaissStore, which utilizes the `faiss` library for rapid similarity search. We also employed the `OpenAiEmbeddingClient` to get the semantic embeddings for the dog breeds. Depending on your needs, you can use a different built-in store or create [a custom one](../how-to/use_custom_similarity_store.md).

## Using the Similarity Index

You can use the index with a custom fetcher [the same way](../quickstart/quickstart2.md) as you would with a built-in fetcher. The similarity index will map user input to the closest matching value from your data source, allowing you to deliver more precise responses to user queries. Remember to frequently update the similarity index with new values from your data source to maintain its relevance. You can accomplish this by calling the `update` method on the similarity index.

```python
await breeds_similarity.update()
```

Then, you can use the similarity index to find the most similar value to a user input and deliver a response based on that value.

```python
print(await breeds_similarity.similar("bagle"))
```

This will return the most similar dog breed to "bagle" based on the data retrieved from the dog.ceo API - in this case, "beagle".

In general, instead of directly calling the similarity index, you would usually use it to annotate arguments to views, as demonstrated in the [Quickstart guide](../quickstart/quickstart2.md).