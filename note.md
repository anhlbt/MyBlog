**Elasticsearch Attachment Plugin**
The attachment plugin lets Elasticsearch accept a base64-encoded document and index its contents for easy searching. This is useful for searching PDF or rich text documents with minimal overhead.

Install the ingest-attachment plugin using the elasticsearch-plugin tool:

sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install ingest-attachment
Restart elasticsearch:

sudo systemctl restart elasticsearch
Confirm that the plugin is installed as expected by using the _cat API:

GET /_cat/plugins
The ingest-attachment plugin should be under the list of installed plugins.

In order to use the attachment plugin, a pipeline must be used to process base64-encoded data in the field of a document. An ingest pipeline is a way of performing additional steps when indexing a document in Elasticsearch. While Elasticsearch comes pre-installed with some pipeline processors (which can perform actions such as removing or adding fields), the attachment plugin installs an additional processor that can be used when defining a pipeline.

```POST _analyze
{
  "analyzer": "whitespace",
  "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
}```

**Some link reference**
https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html
https://github.com/duydo/elasticsearch-analysis-vietnamese
https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis.html
https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-custom-analyzer.html





images = response.xpath("//*[contains(@class, 'prd-imageBoxLayout ui-border')]//img[@class='prd-image']/@src")
image_urls = images.extract()
image_url = image_urls[0]

a

start redis rq: rq worker madblog-tasks