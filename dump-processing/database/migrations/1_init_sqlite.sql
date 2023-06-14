--PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS article (
    id INTEGER PRIMARY KEY,
    title varblob(256) NOT NULL UNIQUE,
    visited boolean NOT NULL,
    component_id int,
    component_level int,
    predecessor varblob(256) REFERENCES article(title)
);

CREATE INDEX IF NOT EXISTS idx_article_title ON article(title);
CREATE INDEX unreached_article_idx ON article (component_id, visited) WHERE component_id is null and visited=1;

CREATE VIRTUAL TABLE IF NOT EXISTS article_title_search USING FTS5(title);

CREATE TABLE IF NOT EXISTS article_component (
    component_id int not null,
    starting_article integer not null,
    FOREIGN KEY (starting_article) REFERENCES article(title) ON DELETE CASCADE,
    primary key (component_id)
);

CREATE TABLE IF NOT EXISTS article_component_connects (
    component_id int not null,
    connects_to_id int not null,
    from_article integer NOT NULL, -- last article from component_id that goes to another component
    FOREIGN KEY (from_article) REFERENCES article(title) ON DELETE CASCADE,
    FOREIGN KEY (component_id) REFERENCES article_component(component_id) ON DELETE CASCADE,
    FOREIGN KEY (connects_to_id) REFERENCES  article_component(component_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_acc_comb ON article_component_connects(component_id, connects_to_id);

CREATE TABLE IF NOT EXISTS article_link_edge_directed (
    from_article integer NOT NULL,
    to_article integer NOT NULL,
    CONSTRAINT check_col_not_eq CHECK (from_article <> to_article),
    FOREIGN KEY (from_article) REFERENCES article(title) ON DELETE CASCADE,
    FOREIGN KEY (to_article) REFERENCES article(title) ON DELETE CASCADE,
    UNIQUE (from_article, to_article)
);

CREATE INDEX IF NOT EXISTS idx_article_outbound ON article_link_edge_directed(from_article);
CREATE INDEX IF NOT EXISTS idx_article_inbound ON article_link_edge_directed(to_article);

CREATE TABLE IF NOT EXISTS redirect (
    from_article integer NOT NULL,
    to_article integer NOT NULL,
    FOREIGN KEY (from_article) REFERENCES article(title) ON DELETE CASCADE,
    FOREIGN KEY (to_article) REFERENCES article(title) ON DELETE CASCADE,
    PRIMARY KEY (from_article)
);
