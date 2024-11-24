<template>
	<div>
		<h3>Book List</h3>
		<!-- Error Message -->
		<div v-if="errorMessage" class="alert alert-danger" role="alert">
			{{ errorMessage }}
		</div>
		<!-- Not Found Message -->
		<div
			v-else-if="books.length === 0"
			class="alert alert-warning"
			role="alert"
		>
			No books found.
		</div>
		<!-- Books List -->
		<ul
			v-else
			class="shadow-sm list-group overflow-auto mt-4"
			style="max-height: 400px"
		>
			<li
				class="list-group-item d-flex justify-content-between align-items-center"
				v-for="book in books"
				:key="book.id"
			>
				<div>
          <div class="d-flex align-items-center mb-2">
            <span class="badge bg-secondary me-2">#{{ book.id }}</span>
            <h5 class="mb-0">{{ book.title }}</h5>
          </div>
					<p>{{ book.description }}</p>
					<small>Published Date: {{ book.published_date }}</small>
				</div>
				<div>
					<button
						class="btn btn-sm btn-primary me-2"
						@click="editBook(book)"
					>
						Edit
					</button>
					<button
						class="btn btn-sm btn-danger"
						@click="confirmDeleteBook(book.id)"
					>
						Delete
					</button>
				</div>
			</li>
		</ul>
	</div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2"; // Import SweetAlert2

export default {
	props: ["books"],
	data() {
		return {
			errorMessage: null, // Holds error messages if any
		};
	},
	methods: {
		confirmDeleteBook(bookId) {
			Swal.fire({
				title: "Are you sure?",
				text: "Do you want to delete this book? This action cannot be undone.",
				icon: "warning",
				showCancelButton: true,
				confirmButtonText: "Yes, delete it!",
				cancelButtonText: "Cancel",
				reverseButtons: true, // Cancel button first
			}).then((result) => {
				if (result.isConfirmed) {
					this.deleteBook(bookId);
				}
			});
		},
		deleteBook(bookId) {
			axios
				.delete(`/api/books/${bookId}/delete/`)
				.then(() => {
					Swal.fire({
						title: "Deleted!",
						text: "The book has been deleted successfully.",
						icon: "success",
						confirmButtonText: "OK",
					});
					this.$emit("book-updated");
				})
				.catch((error) => {
					this.errorMessage =
						"Failed to delete the book. Please try again.";
					Swal.fire({
						title: "Error!",
						text: "Failed to delete the book. Please try again.",
						icon: "error",
						confirmButtonText: "OK",
					});
					console.error(error);
				});
		},
		editBook(book) {
			this.$emit("edit-book", book); // Emit to parent to pass the book being edited
		},
	},
	watch: {
		books: {
			immediate: true,
			handler(newBooks) {
				if (newBooks.length === 0) {
					this.errorMessage = null; // Clear any error messages if data is empty
				}
			},
		},
	},
};
</script>
