import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, type TopicDetail as TopicDetailType } from "../lib/api";
import { useI18n } from "../lib/i18n";
import { ENTITY_ICONS } from "../components/ui/TopicCard";

function fmtDate(iso: string, locale: string) {
  return new Date(iso).toLocaleDateString(locale === "zh" ? "zh-CN" : "en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function TopicDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const { t, locale } = useI18n();
  const [topic, setTopic] = useState<TopicDetailType | null>(null);
  const [err, setErr] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (!slug) return;
    api
      .getTopicDetail(slug, locale)
      .then(setTopic)
      .catch(() => setErr(true));
  }, [slug, locale]);

  if (err) {
    return (
      <div className="empty">
        <h3>{t("detail.not_found")}</h3>
        <p>
          <Link to="/" className="back-link">
            {t("detail.back")}
          </Link>
        </p>
      </div>
    );
  }

  if (!topic) {
    return <div className="empty"><p>{t("detail.loading")}</p></div>;
  }

  function handleSave() {
    if (!topic) return;
    api.saveTopic(topic.id);
    setSaved(true);
  }

  return (
    <>
      <Link to="/" className="back-link">
        {t("detail.back")}
      </Link>

      <div className="detail-header">
        <h1>{topic.title}</h1>
        <div className="detail-meta">
          <span className="badge badge-heat">🔥 {topic.heat_score}</span>
          <span className={`badge badge-${topic.freshness}`}>
            {topic.freshness === "rising" ? t("freshness.rising") : topic.freshness === "fading" ? t("freshness.fading") : t("freshness.stable")}
          </span>
          <span className="badge badge-region">
            {topic.region === "domestic" ? t("region.domestic") : t("region.international")}
          </span>
          <span className="badge badge-category">{t(`cat.${topic.category}` as any)}</span>
          <span className="badge" style={{ background: "#f0f0f0", color: "#555" }}>
            {topic.source_count} {topic.source_count !== 1 ? t("card.sources") : t("card.source")}
          </span>
        </div>
        <p className="detail-summary">{topic.summary}</p>
        <button className={`btn ${saved ? "btn-saved" : "btn-primary"}`} onClick={handleSave}>
          {saved ? t("detail.saved_topic") : t("detail.save_topic")}
        </button>
      </div>

      {topic.timeline.length > 0 && (
        <div className="detail-section">
          <h2>{t("detail.timeline")}</h2>
          <div className="timeline">
            {topic.timeline.map((tl, i) => (
              <div key={i} className="timeline-item">
                <h4>{tl.title}</h4>
                <div className="tl-meta">
                  {fmtDate(tl.timestamp, locale)} &middot; {tl.source}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {topic.entities.length > 0 && (
        <div className="detail-section">
          <h2>{t("detail.entities")}</h2>
          <div className="entity-list">
            {topic.entities.map((e, i) => (
              <span key={i} className="entity-tag">
                <span className="et-icon">{ENTITY_ICONS[e.entity_type] ?? "·"}</span>
                {e.name}
              </span>
            ))}
          </div>
        </div>
      )}

      {topic.sources.length > 0 && (
        <div className="detail-section">
          <h2>{t("detail.sources")}</h2>
          <div className="source-list">
            {topic.sources.map((s, i) => (
              <div key={i} className="source-item">
                <h4>
                  <a href={s.url} target="_blank" rel="noopener noreferrer">
                    {s.title}
                  </a>
                </h4>
                <div className="src-pub">
                  {s.publisher} &middot; {fmtDate(s.publish_time, locale)}
                </div>
                <div className="src-snippet">{s.snippet}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
}
