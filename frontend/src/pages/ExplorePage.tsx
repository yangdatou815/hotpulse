import { useEffect, useState } from "react";
import { api, type TopicSummary } from "../lib/api";
import { useI18n } from "../lib/i18n";
import { TopicCard } from "../components/ui/TopicCard";

const REGIONS = ["all", "domestic", "international"] as const;
const CATEGORIES = ["all", "politics", "economy", "technology", "society", "business", "culture"] as const;
const SORTS = ["heat", "freshness"] as const;

const FEATURED_TAGS = [
  { tag: "us-iran-conflict", labelKey: "tag.us_iran" as const },
] as const;

export function ExplorePage() {
  const { t, locale } = useI18n();
  const [topics, setTopics] = useState<TopicSummary[]>([]);
  const [region, setRegion] = useState("all");
  const [category, setCategory] = useState("all");
  const [activeTag, setActiveTag] = useState<string | null>(null);
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

  return (
    <>
      <h1 className="page-title">{t("explore.title")}</h1>
      <p className="page-subtitle">{t("explore.subtitle")}</p>

      <div className="featured-tags">
        {FEATURED_TAGS.map((ft) => (
          <button
            key={ft.tag}
            className={`featured-pill${activeTag === ft.tag ? " active" : ""}`}
            onClick={() => setActiveTag((prev) => (prev === ft.tag ? null : ft.tag))}
          >
            {t(ft.labelKey)}
          </button>
        ))}
      </div>

      <div className="search-bar">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={t("search.filter_placeholder")}
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
          <h3>{t("explore.no_match")}</h3>
          <p>{t("explore.no_match_hint")}</p>
        </div>
      ) : (
        <div className="topic-grid">
          {topics.map((t) => (
            <TopicCard key={t.id} topic={t} />
          ))}
        </div>
      )}
    </>
  );
}
