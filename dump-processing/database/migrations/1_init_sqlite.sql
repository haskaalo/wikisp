--PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS article (
    title varblob(256) NOT NULL,
    visited boolean NOT NULL,
    PRIMARY KEY (title)
);

CREATE TABLE IF NOT EXISTS article_link_edge_directed (
    from_article varblob(256) NOT NULL,
    to_article varblob(256) NOT NULL,
    CONSTRAINT check_col_not_eq CHECK (from_article <> to_article),
    FOREIGN KEY (from_article) REFERENCES article(title) ON DELETE CASCADE,
    FOREIGN KEY (to_article) REFERENCES article(title) ON DELETE CASCADE,
    UNIQUE (from_article, to_article)
);

CREATE TABLE IF NOT EXISTS redirect (
    from_article varblob(256) NOT NULL,
    to_article varblob(256) NOT NULL,
    PRIMARY KEY (from_article)
);