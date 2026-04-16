import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Layout } from "../components/layout/Layout";
import { HomePage } from "../pages/HomePage";
import { TopicDetailPage } from "../pages/TopicDetailPage";
import { ExplorePage } from "../pages/ExplorePage";
import { SavedPage } from "../pages/SavedPage";

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="topics/:slug" element={<TopicDetailPage />} />
          <Route path="explore" element={<ExplorePage />} />
          <Route path="saved" element={<SavedPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
