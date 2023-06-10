package database

import (
	"log"
	"os"

	_ "github.com/glebarez/go-sqlite"
	"github.com/jmoiron/sqlx"
)

var (
	db *sqlx.DB
)

func InitDatabase() {
	var err error
	path := os.Getenv("SQLITE3_DB_PATH")
	log.Printf("Opening SQLite database at %s", path)

	db, err = sqlx.Connect("sqlite", path)
	if err != nil {
		log.Fatal(err)
	}
	log.Println("Connected to SQLITE database")
}

func CloseDatabase() {
	_ = db.Close()
}

type AdjacentArticle struct {
	FinalDestID    int `db:"finalDest" json:"final"`
	OriginalDestID int `db:"originalDest" json:"original"`
}

func GetAdjacentArticles(articleID int) ([]AdjacentArticle, error) {
	articles := []AdjacentArticle{}

	query := `
			SELECT COALESCE(r.to_article, aled.to_article) as finalDest, aled.to_article as originalDest FROM article_link_edge_directed aled
			LEFT JOIN redirect r ON aled.to_article=r.from_article
			WHERE aled.from_article=?
	`

	err := db.Select(&articles, query, articleID)

	return articles, err
}

type ArticleInfo struct {
	ID          int `db:"id"`
	ComponentID int `db:"component_id"`
}

func GetArticleInfoByTitle(title string) (ArticleInfo, error) {
	query := `
			SELECT COALESCE(r.to_article, a.id) as id, COALESCE(ca.component_id, a.component_id) as component_id FROM article a
			LEFT JOIN redirect r ON r.from_article=a.id
			LEFT JOIN article ca ON ca.id=r.to_article
			WHERE a.title=?
	`
	result := ArticleInfo{}
	err := db.Get(&result, query, title)

	return result, err
}

type ArticleTitle struct {
	title string `db:"title"`
}

func GetArticleTitleByID(id int) (string, error) {
	query := "SELECT title FROM article WHERE id=?"
	result := ArticleTitle{}

	err := db.Get(&result, query, id)

	return result.title, err
}

type Component struct {
	ID int `db:"id"`
}

func GetAdjacentComponents(componentID int) ([]Component, error) {
	query := "SELECT DISTINCT connects_to_id as id FROM article_component_connects WHERE component_id=?"

	var result []Component

	err := db.Select(&result, query, componentID)

	return result, err
}

type ArticleID struct {
	ID int `db:"id"`
}

func GetArticleIDList() (*[]ArticleID, error) {
	query := "SELECT id FROM article WHERE visited=1"
	result := new([]ArticleID)

	err := db.Select(result, query)

	return result, err
}

func GetArticleComponentIDList() (*[]Component, error) {
	query := "SELECT component_id as id FROM article_component"
	result := new([]Component)

	err := db.Select(result, query)

	return result, err

}

type Redirect struct {
	From int `db:"from_article"`
	To   int `db:"to_article"`
}

func GetRedirectList() (*[]Redirect, error) {
	query := "SELECT from_article, to_article FROM redirect"
	result := new([]Redirect)

	err := db.Select(result, query)

	return result, err
}
