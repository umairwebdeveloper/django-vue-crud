<template>
	<div>
		<h3 class="mb-4">
			{{ isEditing ? "Edit Author-Book" : "Add Author-Book" }}
		</h3>
		<form
			@submit.prevent="submitForm"
			class="card p-3"
			style="height: 400px"
		>
			<div class="mb-3">
				<label for="author" class="form-label">Author</label>
				<select
					id="author"
					v-model="form.author_id"
					class="form-select"
					required
				>
					<option value="" disabled>Select an author</option>
					<option
						v-for="author in authors"
						:key="author.id"
						:value="author.id"
					>
						{{ author.name }}
					</option>
				</select>
			</div>
			<div class="mb-3">
				<label for="book" class="form-label">Book</label>
				<select
					id="book"
					v-model="form.book_id"
					class="form-select"
					required
				>
					<option value="" disabled>Select a book</option>
					<option
						v-for="book in books"
						:key="book.id"
						:value="book.id"
					>
						{{ book.title }}
					</option>
				</select>
			</div>
			<div class="mb-3">
				<label for="contribution_percentage" class="form-label"
					>Contribution Percentage</label
				>
				<input
					type="number"
					id="contribution_percentage"
					v-model="form.contribution_percentage"
					class="form-control"
					placeholder="Enter contribution percentage"
				/>
			</div>
			<div>
				<button type="submit" class="btn btn-primary">
					{{ isEditing ? "Update Relationship" : "Add Relationship" }}
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
    authorBook: {
      type: Object,
      default: null,
    },
    authors: {
      type: Array,
      required: true,
    },
    books: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      form: {
        author_id: "",
        book_id: "",
        contribution_percentage: "",
      },
    };
  },
  computed: {
    isEditing() {
      return !!this.authorBook;
    },
  },
  watch: {
    authorBook: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.form.author_id = newVal.author_id;
          this.form.book_id = newVal.book_id;
          this.form.contribution_percentage = newVal.contribution_percentage;
        } else {
          this.resetForm();
        }
      },
    },
  },
  methods: {
    submitForm() {
      if (this.isEditing) {
        axios
          .put(`/api/author-books/${this.authorBook.id}/update/`, this.form)
          .then(() => {
            Swal.fire({
              title: "Success!",
              text: "Author-Book relationship updated successfully.",
              icon: "success",
              confirmButtonText: "OK",
            });
            this.$emit("author-book-updated");
            this.resetForm();
          })
          .catch((error) => {
            this.handleError(error);
          });
      } else {
        axios
          .post("/api/author-books/create/", this.form)
          .then(() => {
            Swal.fire({
              title: "Success!",
              text: "Author-Book relationship added successfully.",
              icon: "success",
              confirmButtonText: "OK",
            });
            this.$emit("author-book-added");
            this.resetForm();
          })
          .catch((error) => {
            this.handleError(error);
          });
      }
    },
    handleError(error) {
      if (error.response) {
        // Backend returned an error response
        const { status, data } = error.response;
        if (status === 400) {
          Swal.fire({
            title: "Validation Error!",
            text: data.error || "Please check the form fields and try again.",
            icon: "warning",
            confirmButtonText: "OK",
          });
        } else if (status === 404) {
          Swal.fire({
            title: "Not Found!",
            text: "The requested resource could not be found.",
            icon: "error",
            confirmButtonText: "OK",
          });
        } else if (status === 500) {
          Swal.fire({
            title: "Server Error!",
            text: "An unexpected error occurred on the server. Please try again later.",
            icon: "error",
            confirmButtonText: "OK",
          });
        } else {
          Swal.fire({
            title: "Error!",
            text: data.error || "Something went wrong. Please try again.",
            icon: "error",
            confirmButtonText: "OK",
          });
        }
      } else {
        // Network or other errors
        Swal.fire({
          title: "Network Error!",
          text: "Unable to connect to the server. Please check your internet connection and try again.",
          icon: "error",
          confirmButtonText: "OK",
        });
      }
    },
    resetForm() {
      this.form = {
        author_id: "",
        book_id: "",
        contribution_percentage: "",
      };
      this.$emit("cancel-edit");
    },
    cancelEdit() {
      this.resetForm();
    },
  },
};
</script>
