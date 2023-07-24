package database

import (
	"database/sql"
	"fmt"
	_ "github.com/glebarez/go-sqlite"
	"github.com/go-redis/redis"
	"github.com/jmoiron/sqlx"
	"log"
	"os"
	"strings"
)

var (
	db *sqlx.DB
	r  *redis.Client
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

func InitRedis() {
	r = redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%v", os.Getenv("REDIS_HOST"), os.Getenv("REDIS_PORT")),
		Password: os.Getenv("REDIS_PASSWORD"),
	})
}

type SearchArticleResult struct {
	Title string `db:"title"`
}

func sanitizeFTS(query string) string {
	return strings.ReplaceAll(query, "\"", "\"\"")
}

func SearchArticle(searchQuery string) ([]string, error) {
	queryResult := []SearchArticleResult{}

	query := `SELECT distinct title collate nocase as title FROM article_title_search
		WHERE title MATCH '^' || '"' || ? || '"' limit 10`

	err := db.Select(&queryResult, query, sanitizeFTS(searchQuery))
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
	ID          int           `db:"id"`
	ComponentID sql.NullInt64 `db:"component_id"`
}

func GetArticleIDsFromTitle(title string) (int, int, error) {
	queryResult := ArticleIDFromTitle{}
	query := `SELECT id, component_id FROM article where title=?`

	err := db.Get(&queryResult, query, title)
	if err != nil {
		return -1, -1, err
	}

	if !queryResult.ComponentID.Valid {
		query := `SELECT id, component_id FROM article where id=?`
		err = db.Get(&queryResult, query, RedirectMap[queryResult.ID])
		if err != nil {
			return -1, -1, err
		}
	}

	return queryResult.ID, int(queryResult.ComponentID.Int64), nil
}

func GetArticleTitleFromID(ID int) (string, error) {
	queryResult := SearchArticleResult{}

	query := "SELECT title FROM article WHERE id=?"

	err := db.Get(&queryResult, query, ID)
	if err != nil {
		return "", err
	}

	return queryResult.Title, nil
}

func GetRandomArticles(limit int) ([]string, error) {
	queryResult := []SearchArticleResult{}
	query := "SELECT title FROM article ORDER BY RANDOM() LIMIT ?"
	err := db.Select(&queryResult, query, limit)
	if err != nil {
		return nil, err
	}

	result := []string{}
	for _, article := range queryResult {
		result = append(result, article.Title)
	}

	return result, nil
}
