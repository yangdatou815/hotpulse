import { Link } from "react-router-dom";
import type { TopicSummary } from "../../lib/api";
import { useI18n } from "../../lib/i18n";

const ENTITY_ICONS: Record<string, string> = {
  person: "👤",
  org: "🏛",
  location: "📍",
};

export function TopicCard({
  topic,
  onSave,
  saved,
}: {
  topic: TopicSummary;
  onSave?: (id: string) => void;
  saved?: boolean;
}) {
  const { t } = useI18n();

  function freshnessLabel(f: string) {
    if (f === "rising") return t("freshness.rising");
    if (f === "fading") return t("freshness.fading");
    return t("freshness.stable");
  }

  return (
    <Link to={`/topics/${topic.slug}`} className="topic-card">
      <h3>{topic.title}</h3>
      <p>{topic.summary}</p>
      <div className="card-meta">
        <span className="badge badge-heat">🔥 {topic.heat_score}</span>
        <span className={`badge badge-${topic.freshness}`}>{freshnessLabel(topic.freshness)}</span>
        <span className="badge badge-region">{topic.region === "domestic" ? t("region.domestic") : t("region.international")}</span>
        <span className="badge badge-category">{t(`cat.${topic.category}` as any)}</span>
        {topic.tags && topic.tags.length > 0 && topic.tags.map((tag) => (
          <span key={tag} className="badge badge-tag">#{tag}</span>
        ))}
      </div>
      {onSave && (
        <button
          className={`btn ${saved ? "btn-saved" : ""}`}
          style={{ marginTop: 12, alignSelf: "flex-start" }}
          onClick={(e) => {
            e.preventDefault();
            onSave(topic.id);
          }}
        >
          {saved ? t("card.saved") : t("card.save")}
        </button>
      )}
    </Link>
  );
}

export { ENTITY_ICONS };
