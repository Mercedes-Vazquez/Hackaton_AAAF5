import { render, screen } from "@testing-library/vue";
import HomePage from "@/views/Home/HomePage.vue";

test("show initial message", () => {
  render(HomePage);
  expect(screen.getByText("This is the home page")).toBeInTheDocument();
  expect(screen.getByText("Hello, world!")).toBeInTheDocument();
});
