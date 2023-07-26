import * as React from "react";
import { createRoot } from "react-dom/client";
import App from "./app";
import logo from "@home/static/logo.jpg";


console.log(logo);

const container = document.getElementById("root-app");
const root = createRoot(container);

root.render(<App/>);