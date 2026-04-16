import { useEffect, useState } from "react";
import { api, type TopicSummary } from "../lib/api";
import { useI18n } from "../lib/i18n";
import { TopicCard } from "../components/ui/TopicCard";

export function SavedPage() {
  const { t, locale } = useI18n();
  const [topics, setTopics] = useState<TopicSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .listSaved(locale)
      .then(setTopics)
      .catch(() => setTopics([]))
      .finally(() => setLoading(false));
  }, [locale]);

  function handleRemove(id: string) {
    api.removeSaved(id);
    setTopics((prev) => prev.filter((item) => item.id !== id));
  }

  return (
    <>
      <h1 className="page-title">{t("saved.title")}</h1>
      <p className="page-subtitle">{t("saved.subtitle")}</p>

      {loading ? (
        <div className="empty"><p>{t("detail.loading")}</p></div>
      ) : topics.length === 0 ? (
        <div className="empty">
          <h3>{t("saved.empty")}</h3>
          <p>{t("saved.empty_hint")}</p>
        </div>
      ) : (
        <div className="topic-grid">
          {topics.map((topic) => (
            <div key={topic.id} style={{ position: "relative" }}>
              <TopicCard topic={topic} />
              <button
                className="btn"
                style={{ position: "absolute", top: 12, right: 12, fontSize: "0.75rem" }}
                onClick={() => handleRemove(topic.id)}
              >
                {t("saved.remove")}
              </button>
            </div>
          ))}
        </div>
      )}
    </>
  );
}
