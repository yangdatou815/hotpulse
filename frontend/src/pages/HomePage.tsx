import { useEffect, useState } from "react";
import { api, type TopicSummary } from "../lib/api";
import { useI18n } from "../lib/i18n";
import { TopicCard } from "../components/ui/TopicCard";

const REGIONS = ["all", "domestic", "international"] as const;
const CATEGORIES = ["all", "politics", "economy", "technology", "society", "business", "culture"] as const;

const FEATURED_TAGS = [
  { tag: "us-iran-conflict", labelKey: "tag.us_iran" as const },
] as const;

export function HomePage() {
  const { t, locale } = useI18n();
  const [topics, setTopics] = useState<TopicSummary[]>([]);
  const [region, setRegion] = useState<string>("all");
  const [category, setCategory] = useState<string>("all");
  const [activeTag, setActiveTag] = useState<string | null>(null);
  const [saved, setSaved] = useState<Set<string>>(new Set());
  const [query, setQuery] = useState("");

  useEffect(() => {
    const params: Record<string, string> = { lang: locale };
    if (region !== "all") params.region = region;
    if (category !== "all") params.category = category;
    if (activeTag) params.tag = activeTag;

    const req = query.trim()
      ? api.search(query, params)
      : api.listTopics(params);

    req.then((d) => setTopics(d.items)).catch(() => setTopics([]));
  }, [region, category, query, activeTag, locale]);

  function handleSave(id: string) {
    api.saveTopic(id);
    setSaved((prev) => new Set(prev).add(id));
  }

  function toggleTag(tag: string) {
    setActiveTag((prev) => (prev === tag ? null : tag));
  }

  return (
    <>
      <div className="hero">
        <h2>{t("hero.title")}</h2>
        <p>{t("hero.subtitle")}</p>
      </div>

      <div className="featured-tags">
        {FEATURED_TAGS.map((ft) => (
          <button
            key={ft.tag}
            className={`featured-pill${activeTag === ft.tag ? " active" : ""}`}
            onClick={() => toggleTag(ft.tag)}
          >
            {t(ft.labelKey)}
          </button>
        ))}
      </div>

      <div className="search-bar">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={t("search.placeholder")}
        />
      </div>

      <div className="filters">
        {REGIONS.map((r) => (
          <button
            key={r}
            className={`pill${region === r ? " active" : ""}`}
            onClick={() => setRegion(r)}
          >
            {r === "all" ? t("region.all") : r === "domestic" ? t("region.domestic") : t("region.international")}
          </button>
        ))}
        <span style={{ width: 8 }} />
        {CATEGORIES.map((c) => (
          <button
            key={c}
            className={`pill${category === c ? " active" : ""}`}
            onClick={() => setCategory(c)}
          >
            {t(`cat.${c}` as any)}
          </button>
        ))}
      </div>

      {topics.length === 0 ? (
        <div className="empty">
          <h3>{t("home.no_topics")}</h3>
          <p>{t("home.no_topics_hint")}</p>
        </div>
      ) : (
        <div className="topic-grid">
          {topics.map((t) => (
            <TopicCard
              key={t.id}
              topic={t}
              onSave={handleSave}
              saved={saved.has(t.id)}
            />
          ))}
        </div>
      )}
    </>
  );
}
