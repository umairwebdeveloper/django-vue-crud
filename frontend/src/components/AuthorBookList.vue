<template>
	<div>
		<h3>Author-Book Relationships</h3>
		<!-- No Relationships Found -->
		<div v-if="!authorBooks.length" class="alert alert-warning mt-4" role="alert">
			No author-book relationships found.
		</div>
		<!-- Relationships List -->
		<ul
			v-else
			class="shadow-sm list-group overflow-auto mt-4"
			style="max-height: 400px"
		>
			<li
				class="list-group-item d-flex justify-content-between align-items-center"
				v-for="authorBook in authorBooks"
				:key="authorBook.id"
			>
				<div>
					<strong>Author:</strong> {{ authorBook.author__name }}<br />
					<strong>Book:</strong> {{ authorBook.book__title }}<br />
					<strong>Contribution:</strong>
					{{ authorBook.contribution_percentage }}%
				</div>
				<div>
					<button
						class="btn btn-sm btn-primary me-2"
						@click="editAuthorBook(authorBook)"
					>
						Edit
					</button>
					<button
						class="btn btn-sm btn-danger"
						@click="confirmDeleteAuthorBook(authorBook.id)"
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
	props: ["authorBooks"],
	methods: {
		confirmDeleteAuthorBook(authorBookId) {
			Swal.fire({
				title: "Are you sure?",
				text: "Do you want to delete this author-book relationship? This action cannot be undone.",
				icon: "warning",
				showCancelButton: true,
				confirmButtonText: "Yes, delete it!",
				cancelButtonText: "Cancel",
				reverseButtons: true,
			}).then((result) => {
				if (result.isConfirmed) {
					this.deleteAuthorBook(authorBookId);
				}
			});
		},
		deleteAuthorBook(authorBookId) {
			axios
				.delete(`/api/author-books/${authorBookId}/delete/`)
				.then(() => {
					Swal.fire({
						title: "Deleted!",
						text: "The author-book relationship has been deleted successfully.",
						icon: "success",
						confirmButtonText: "OK",
					});
					this.$emit("author-book-updated");
				})
				.catch(() => {
					Swal.fire({
						title: "Error!",
						text: "Failed to delete the author-book relationship. Please try again.",
						icon: "error",
						confirmButtonText: "OK",
					});
				});
		},
		editAuthorBook(authorBook) {
			this.$emit("edit-author-book", authorBook);
		},
	},
};
</script>
