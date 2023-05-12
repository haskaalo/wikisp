CREATE TABLE article (
    title varbinary(256) NOT NULL,
    PRIMARY KEY (title)
);

CREATE TABLE article_link_edge_directed (
    id SERIAL NOT NULL,
    from_article varbinary(256) REFERENCES article(title) ON DELETE CASCADE,
    to_article varbinary(256) REFERENCES article(title) ON DELETE CASCADE,
    UNIQUE (from_article, to_article),
    PRIMARY KEY (id)
);
