from api.datasets import list_dataset_names


def keyword_search(keyword):
    """
        Performs a simple keyword search against the list of datasets and returns those which include that keyword
    """

    datasets = list_dataset_names()

    matching_datasets = [d for d in datasets if keyword in d]

    return matching_datasets
