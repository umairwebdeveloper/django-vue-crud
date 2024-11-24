<template>
	<div>
		<h3 class="mb-4">{{ isEditing ? "Edit Book" : "Add Book" }}</h3>
		<form
			@submit.prevent="submitForm"
			class="card p-3"
			style="height: 400px"
		>
			<div class="mb-3">
				<label for="title" class="form-label">Title</label>
				<input
					type="text"
					id="title"
					v-model="form.title"
					class="form-control"
					placeholder="Enter book title"
					required
				/>
			</div>
			<div class="mb-3">
				<label for="description" class="form-label">Description</label>
				<textarea
					id="description"
					v-model="form.description"
					class="form-control"
					placeholder="Enter book description"
				></textarea>
			</div>
			<div class="mb-3">
				<label for="published_date" class="form-label">Published Date</label>
				<input
					type="date"
					id="published_date"
					v-model="form.published_date"
					class="form-control"
					placeholder="Enter published date"
				/>
			</div>
			<div>
				<button type="submit" class="btn btn-primary">
					{{ isEditing ? "Update Book" : "Add Book" }}
				</button>
				<button
					type="button"
					v-if="isEditing"
					class="btn btn-secondary ms-2"
					@click="cancelEdit"
				>
					Cancel
				</button>
			</div>
		</form>
	</div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2"; // Import SweetAlert2

export default {
	props: {
		book: {
			type: Object,
			default: null, // Null means we're adding a new book
		},
	},
	data() {
		return {
			form: {
				title: "",
				description: "",
				published_date: "",
			},
		};
	},
	computed: {
		isEditing() {
			return !!this.book; // If `book` is passed, we're editing
		},
	},
	watch: {
		// When `book` changes, populate the form fields
		book: {
			immediate: true,
			handler(newVal) {
				if (newVal) {
					this.form.title = newVal.title;
					this.form.description = newVal.description;
					this.form.published_date = newVal.published_date;
				} else {
					this.resetForm();
				}
			},
		},
	},
	methods: {
		submitForm() {
			if (this.isEditing) {
				// Update Book
				axios
					.put(`/api/books/${this.book.id}/update/`, this.form)
					.then(() => {
						Swal.fire({
							title: "Success!",
							text: "Book updated successfully.",
							icon: "success",
							confirmButtonText: "OK",
						});
						this.$emit("book-updated");
						this.resetForm();
					})
					.catch(() => {
						Swal.fire({
							title: "Error!",
							text: "Failed to update the book. Please try again.",
							icon: "error",
							confirmButtonText: "OK",
						});
					});
			} else {
				// Create Book
				axios
					.post("/api/books/create/", this.form)
					.then(() => {
						Swal.fire({
							title: "Success!",
							text: "Book added successfully.",
							icon: "success",
							confirmButtonText: "OK",
						});
						this.$emit("book-added");
						this.resetForm();
					})
					.catch(() => {
						Swal.fire({
							title: "Error!",
							text: "Failed to add the book. Please try again.",
							icon: "error",
							confirmButtonText: "OK",
						});
					});
			}
		},
		resetForm() {
			this.form.title = "";
			this.form.description = "";
			this.form.published_date = "";
			this.$emit("cancel-edit"); // Inform parent that editing is canceled
		},
		cancelEdit() {
			this.resetForm();
		},
	},
};
</script>
