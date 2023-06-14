package database

import (
	_ "github.com/glebarez/go-sqlite"
	"github.com/jmoiron/sqlx"
	"log"
	"os"
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

type SearchArticleResult struct {
	Title string `db:"title"`
}

func SearchArticle(searchQuery string) ([]string, error) {
	queryResult := []SearchArticleResult{}
	query := "SELECT distinct title collate nocase as title FROM article_title_search WHERE title MATCH ? limit 10"

	err := db.Select(&queryResult, query, "^"+searchQuery)
	if err != nil {
		return nil, err
	}

	result := make([]string, len(queryResult))
	for i, val := range queryResult {
		result[i] = val.Title
	}

	return result, nil
}

type ArticleIDFromTitle struct {
	ID          int `db:"id"`
	ComponentID int `db:"component_id"`
}

func GetArticleIDsFromTitle(title string) (int, int, error) {
	queryResult := ArticleIDFromTitle{}
	query := "SELECT id, component_id FROM article WHERE title=?"

	err := db.Get(&queryResult, query, title)
	if err != nil {
		return -1, -1, err
	}

	return queryResult.ID, queryResult.ComponentID, nil
}
