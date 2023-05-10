CREATE TABLE article (
    title varchar(256) NOT NULL,
    PRIMARY KEY (title)
);

CREATE TABLE article_link_edge_directed (
    id SERIAL NOT NULL,
    from_article varchar(256) REFERENCES article(title) ON DELETE CASCADE,
    to_article varchar(256) REFERENCES article(title) ON DELETE CASCADE,
    PRIMARY KEY (id)
);
