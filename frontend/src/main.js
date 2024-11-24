import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:8000/";


import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

createApp(App).mount("#app");


