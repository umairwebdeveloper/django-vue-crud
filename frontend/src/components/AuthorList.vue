<template>
  <div>
    <h3>Author List</h3>
    <!-- Error Message -->
    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>
    <!-- Not Found Message -->
    <div v-else-if="authors.length === 0" class="alert alert-warning" role="alert">
      No authors found.
    </div>
    <!-- Authors List -->
    <ul
      v-else
      class="shadow-sm list-group overflow-auto mt-4"
      style="max-height: 300px;"
    >
      <li
        class="list-group-item d-flex justify-content-between align-items-start"
        v-for="author in authors"
        :key="author.id"
      >
        <div class="ms-2 me-auto">
          <div class="d-flex align-items-center">
            <span class="badge bg-secondary me-2">#{{ author.id }}</span>
            <h5 class="mb-0">{{ author.name }}</h5>
          </div>
          <p class="text-muted mt-2">{{ author.bio }}</p>

          <!-- Books List -->
          <div>
            <small class="fw-bold">Books Written:</small>
            <ul class="list-group list-group-flush mt-2">
              <li
                v-for="book in author.books"
                :key="book.id"
                class="list-group-item"
              >
                {{ book.title }}
              </li>
              <li v-if="!author.books || author.books.length === 0" class="list-group-item">
                <span class="text-muted">No books written</span>
              </li>
            </ul>
          </div>
        </div>
        <div>
          <button
            class="btn btn-sm btn-primary mb-2 me-2"
            @click="editAuthor(author)"
          >
            Edit
          </button>
          <button
            class="btn btn-sm btn-danger mb-2"
            @click="confirmDeleteAuthor(author.id)"
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
  props: ["authors"],
  data() {
    return {
      errorMessage: null, // Holds error messages if any
    };
  },
  methods: {
    confirmDeleteAuthor(authorId) {
      Swal.fire({
        title: "Are you sure?",
        text: "Do you want to delete this author? This action cannot be undone.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "Cancel",
        reverseButtons: true, // Cancel button first
      }).then((result) => {
        if (result.isConfirmed) {
          this.deleteAuthor(authorId);
        }
      });
    },
    deleteAuthor(authorId) {
      axios
        .delete(`/api/authors/${authorId}/delete/`)
        .then(() => {
          Swal.fire({
            title: "Deleted!",
            text: "The author has been deleted successfully.",
            icon: "success",
            confirmButtonText: "OK",
          });
          this.$emit("author-updated");
        })
        .catch((error) => {
          this.errorMessage = "Failed to delete the author. Please try again.";
          Swal.fire({
            title: "Error!",
            text: "Failed to delete the author. Please try again.",
            icon: "error",
            confirmButtonText: "OK",
          });
          console.error(error);
        });
    },
    editAuthor(author) {
      this.$emit("edit-author", author); // Emit to parent to pass the author being edited
    },
  },
  watch: {
    authors: {
      immediate: true,
      handler(newAuthors) {
        if (newAuthors.length === 0) {
          this.errorMessage = null; // Clear any error messages if data is empty
        }
      },
    },
  },
};
</script>
