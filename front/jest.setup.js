import "@testing-library/jest-dom";

import api from "@/services/api";

api.fetch = require("node-fetch");
api.prefix = "http://localhost:5000/";
api.showError = false;
global.api = api;
