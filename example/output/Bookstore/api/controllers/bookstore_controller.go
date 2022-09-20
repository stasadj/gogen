/**
  Generated by: silvera
  Date: 2022-09-20 23:08:02
*/
package controllers

import (
	"bookstore/models"
	"bookstore/services"
	"encoding/json"
	"net/http"

	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/mongo"
)

type BookstoreController struct {
	*services.BookstoreService
}

func NewBookstoreController(database *mongo.Database) *BookstoreController {
	return &BookstoreController{
	        BookstoreService: services.NewBookstoreService(database),
	        }
}

 // Auto-generated CRUD methods
func (bookstoreController *BookstoreController) CreateBook() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var book models.Book
		_ = json.NewDecoder(r.Body).Decode(&book)
		w.Header().Set("Content-Type", "application/json")
		if err := json.NewEncoder(w).Encode(bookstoreController.BookstoreService.CreateBook(&book))
		err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
	}
}
func (bookstoreController *BookstoreController) GetBook() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		params := mux.Vars(r)
		w.Header().Set("Content-Type", "application/json")
		if err := json.NewEncoder(w).Encode(bookstoreController.BookstoreService.GetBook(params["id"]))
		err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
	}
}
func (bookstoreController *BookstoreController) UpdateBook() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var book models.Book
		_ = json.NewDecoder(r.Body).Decode(&book)
		w.Header().Set("Content-Type", "application/json")
		if err := json.NewEncoder(w).Encode(bookstoreController.BookstoreService.UpdateBook(&book))
		err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
	}
}
func (bookstoreController *BookstoreController) DeleteBook() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		params := mux.Vars(r)
		w.Header().Set("Content-Type", "application/json")
		if err := json.NewEncoder(w).Encode(bookstoreController.BookstoreService.DeleteBook(params["id"]))
		err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
	}
}

// Auto-generated custom methods
func (bookstoreController *BookstoreController) ListBooks() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		if err := json.NewEncoder(w).Encode(bookstoreController.BookstoreService.ListBooks())
		err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
	}
}
func (bookstoreController *BookstoreController) BookExists() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
	 /*
	 TODO: Implement this function!!!
		params := mux.Vars(r)
		w.Header().Set("Content-Type", "application/json")
		if err := json.NewEncoder(w).Encode(bookstoreController.BookstoreService.BookExists())
		err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
	 */
	}
}
func (bookstoreController *BookstoreController) BookPrice() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
	 /*
	 TODO: Implement this function!!!
		params := mux.Vars(r)
		w.Header().Set("Content-Type", "application/json")
		if err := json.NewEncoder(w).Encode(bookstoreController.BookstoreService.BookPrice())
		err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
	 */
	}
}