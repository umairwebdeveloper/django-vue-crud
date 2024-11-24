<template>
	<div>
		<h3 class="mb-4">{{ isEditing ? "Edit Author" : "Add Author" }}</h3>
		<form
			@submit.prevent="submitForm"
			class="card p-3"
			style="height: 300px"
		>
			<div class="mb-3">
				<label for="name" class="form-label">Name</label>
				<input
					type="text"
					id="name"
					v-model="form.name"
					class="form-control"
					placeholder="Enter auther name"
					required
				/>
			</div>
			<div class="mb-3">
				<label for="bio" class="form-label">Bio</label>
				<textarea
					id="bio"
					v-model="form.bio"
					class="form-control"
					placeholder="Enter auther bio"
				></textarea>
			</div>
			<div>
				<button type="submit" class="btn btn-primary">
					{{ isEditing ? "Update Author" : "Add Author" }}
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
		author: {
			type: Object,
			default: null, // Null means we're adding a new author
		},
	},
	data() {
		return {
			form: {
				name: "",
				bio: "",
			},
		};
	},
	computed: {
		isEditing() {
			return !!this.author; // If `author` is passed, we're editing
		},
	},
	watch: {
		// When `author` changes, populate the form fields
		author: {
			immediate: true,
			handler(newVal) {
				if (newVal) {
					this.form.name = newVal.name;
					this.form.bio = newVal.bio;
				} else {
					this.resetForm();
				}
			},
		},
	},
	methods: {
		submitForm() {
			if (this.isEditing) {
				// Update Author
				axios
					.put(`/api/authors/${this.author.id}/update/`, this.form)
					.then(() => {
						Swal.fire({
							title: "Success!",
							text: "Author updated successfully.",
							icon: "success",
							confirmButtonText: "OK",
						});
						this.$emit("author-updated");
						this.resetForm();
					})
					.catch(() => {
						Swal.fire({
							title: "Error!",
							text: "Failed to update the author. Please try again.",
							icon: "error",
							confirmButtonText: "OK",
						});
					});
			} else {
				// Create Author
				axios
					.post("/api/authors/create/", this.form)
					.then(() => {
						Swal.fire({
							title: "Success!",
							text: "Author added successfully.",
							icon: "success",
							confirmButtonText: "OK",
						});
						this.$emit("author-added");
						this.resetForm();
					})
					.catch(() => {
						Swal.fire({
							title: "Error!",
							text: "Failed to add the author. Please try again.",
							icon: "error",
							confirmButtonText: "OK",
						});
					});
			}
		},
		resetForm() {
			this.form.name = "";
			this.form.bio = "";
			this.$emit("cancel-edit"); // Inform parent that editing is canceled
		},
		cancelEdit() {
			this.resetForm();
		},
	},
};
</script>
