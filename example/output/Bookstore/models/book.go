/**
    Generated by: silvera
    Date: 2022-09-20 23:08:02
*/
package models

type Book struct {
    ID		    string	`bson:"_id,omitempty" json:"id"`
    Isbn	    string	`bson:"isbn" json:"isbn"`
    Title	    string	`bson:"title,omitempty" json:"title"`
    Author	    string	`bson:"author,omitempty" json:"author"`
    Category	    string	`bson:"category" json:"category"`
    Price	    float32	`bson:"price,omitempty" json:"price"`
}