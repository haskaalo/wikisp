# wikisp

[Six Degrees of Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Six_degrees_of_Wikipedia) is a captivating concept inspired by the theory of six degrees of separation, commonly used in social networks, demonstrating that any two Wikipedia articles can be connected within six clicks or fewer. This project specifically focuses on uncovering the shortest path between articles on the English version of Wikipedia, exploring the vast web of interconnected knowledge present on the platform.

This project also allows you to build a clean SQLITE3 database with a adjacency list and partioned graph for easy traversal and use in your own projects.

## Table of contents

- [Requirements](#requirements)
- [Building adjacency links (graph db)](#1-building-wikipedia-link-adjacency-lists)
- [Running the webserver](#2-running-the-webserver)

## Requirements

| Tool| Explanation for why it's needed |
| ---  | ----------- |
| Python 3.x | Used for dump processing |
| Go 1.20 | Used to build serialized adjacency lists and webserver |
| NodeJS v18+ | Needed for development only |
| Docker | Build and run webserver |

## Getting started

### 1. Building Wikipedia link adjacency lists

In order to build Wikipedia link adjacency it is required to download a Wikipedia dump file from [here (~30gb)](https://dumps.wikimedia.org/backup-index.html). The file required to download from Wikipedia archives should be named: `enwiki-xxxxxxxx-pages-articles-multistream.xml.bz2`.

Once downloaded, please set the following environnement variables:

| Name | Description |
| ---  | ----------- |
| OUT_DIR | Path of a directory to put link adjacency lists to |
| WIKI_XML_DUMP | Wikipedia XML dump file path |
| SQLITE3_DB_PATH | Path to a SQLite3 database for informations about adjacency and articles |
| ADJACENCY_LIST_PATH | Path to serialized adjacency list (Should equal to `OUT_DIR`) (Optional if you're not planning to run the webserver) |


To run all the steps for dump processing run this command on a terminal:

```
make dump-processing
```

The following section is a step by step guide on building adjacency lists (Not needed if `make dump-processing` was ran)

#### 1. Parsing dumps to CSV files
After environnement variables are set the first step required to build Wikipedia link adjacency lists is to parse the dumps and write them to a csv file (Note: They are written to a CSV for faster parsing). This is done doing the following command on a terminal:

```
make step1-dp
```

This will create 3 csv files (article.csv, redirect.csv, pagesmentioned.csv) to the directory set by `OUT_DIR`.

* article.csv: Article titles
* redirect.csv: Articles title that redirects to another article
* pagesmentioned.csv: Article A has a link to Article B

#### 2. Writing CSV files to SQLITE3 database
Once the dumps has been processed by step 1, it is necessary to write them to a sqlite3 database to perform some data manipulation such as deleting articles that don't exists, removing redirect loops, knowing which articles are simply aliales to another article, and partioning the graph in step 3.

This is done using the command on a terminal:

```
make step2-dp
```

#### 3. "Partitioning" the graph
Once step 2 is done, the final step required is partioning the graph. This is done to reduce execution time for requests to articles that doesn't have a path.

**NOTE**: Because this is a directed graph, partitioning the graph doesn't allow to know **every** pairs of articles that doesn't have a path but a significant amount.

This is done using the following command:
```
make step3-dp
```

**NOTE**: Don't run this if you want to use the adjacency lists for your own projects.

#### 4. Optional: Building the serialized adjacency lists for the webserver to use

```
make step4-dp
```

#### 5. Optional: Cleaning up the database to reduce size
After step 3, there are some large tables in the database set by `SQLITE3_DB_PATH` such as article_link_edge_directed that will not be used by the webserver. This can be done by running

```
make step5-dp
```

**NOTE**: Running `VACUUM` in the SQLite3 database will reduce the size also.

### 2. Running the webserver

This is for production only. For development check out the development section.

Environment variables needed:

| Name | Description |
| ---  | ----------- |
| ADJACENCY_LIST_PATH | Path to serialized adjacency list directory generated in section 1|
| SQLITE3_DB_DIR | Path to SQLITE3 database directory generated in section 1 |
| RECAPTCHA_SECRET | Google Recaptcha secret |
| RECAPTCHA_SITEKEY | Google Recaptcha site key|

#### 1. Build the webserver image

```
make build-image
```

#### 2. Running the server

```
make run-webapp
```