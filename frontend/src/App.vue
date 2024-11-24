<template>
	<div class="container my-5">
		<h1 class="text-center mb-4">Django & Vue.js CRUD with Bootstrap</h1>
		<!-- Author Management -->
		<div class="row">
			<div class="col-md-6">
				<AuthorForm
					:author="selectedAuthor"
					@author-added="fetchAuthors"
					@author-updated="fetchAuthors"
					@cancel-edit="clearSelectedAuthor"
				/>
			</div>
			<div class="col-md-6">
				<AuthorList
					:authors="authors"
					@author-updated="fetchAuthors"
					@edit-author="setSelectedAuthor"
				/>
			</div>
		</div>
		<hr class="my-5" />
		<!-- Book Management -->
		<div class="row">
			<div class="col-md-6">
				<BookForm
					:book="selectedBook"
					@book-added="fetchBooks"
					@book-updated="fetchBooks"
					@cancel-edit="clearSelectedBook"
				/>
			</div>
			<div class="col-md-6">
				<BookList
					:books="books"
					@book-updated="fetchBooks"
					@edit-book="setSelectedBook"
				/>
			</div>
		</div>
		<hr class="my-5" />
		<!-- AuthorBook Management -->
		<div class="row">
			<div class="col-md-6">
				<AuthorBookForm
					:authorBook="selectedAuthorBook"
					:authors="authors"
					:books="books"
					@author-book-added="fetchAuthorBooks"
					@author-book-updated="fetchAuthorBooks"
					@cancel-edit="clearSelectedAuthorBook"
				/>
			</div>
			<div class="col-md-6">
				<AuthorBookList
					:authorBooks="authorBooks"
					@author-book-updated="fetchAuthorBooks"
					@edit-author-book="setSelectedAuthorBook"
				/>
			</div>
		</div>
	</div>
</template>

<script>
import AuthorList from "./components/AuthorList.vue";
import AuthorForm from "./components/AuthorForm.vue";
import BookForm from "./components/BookForm.vue";
import BookList from "./components/BookList.vue";
import AuthorBookForm from "./components/AuthorBookForm.vue";
import AuthorBookList from "./components/AuthorBookList.vue";
import axios from "axios";

export default {
	data() {
		return {
			authors: [],
			books: [],
			authorBooks: [],
			selectedAuthor: null, // Holds the author being edited
			selectedBook: null, // Holds the book being edited
			selectedAuthorBook: null, // Holds the AuthorBook being edited
		};
	},
	components: {
		AuthorList,
		AuthorForm,
		BookForm,
		BookList,
		AuthorBookForm,
		AuthorBookList,
	},
	methods: {
		// Fetch Authors
		fetchAuthors() {
			axios.get("/api/authors/").then((response) => {
				this.authors = response.data.authors;
			});
		},
		setSelectedAuthor(author) {
			this.selectedAuthor = author; // Set the author to be edited
		},
		clearSelectedAuthor() {
			this.selectedAuthor = null; // Clear the selected author (cancel edit)
		},

		// Fetch Books
		fetchBooks() {
			axios.get("/api/books/").then((response) => {
				this.books = response.data.books;
			});
		},
		setSelectedBook(book) {
			this.selectedBook = book; // Set the book to be edited
		},
		clearSelectedBook() {
			this.selectedBook = null; // Clear the selected book (cancel edit)
		},

		// Fetch AuthorBook Relationships
		fetchAuthorBooks() {
			axios.get("/api/author-books/").then((response) => {
				this.authorBooks = response.data.author_books;
			});
		},
		setSelectedAuthorBook(authorBook) {
			this.selectedAuthorBook = authorBook; // Set the AuthorBook relationship to be edited
		},
		clearSelectedAuthorBook() {
			this.selectedAuthorBook = null; // Clear the selected AuthorBook (cancel edit)
		},
	},
	mounted() {
		this.fetchAuthors();
		this.fetchBooks();
		this.fetchAuthorBooks();
	},
};
</script>
