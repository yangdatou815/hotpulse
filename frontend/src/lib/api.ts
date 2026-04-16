const BASE = import.meta.env.VITE_API_BASE ?? "/api/v1";

export type TopicSummary = {
  id: string;
  slug: string;
  title: string;
  summary: string;
  region: "domestic" | "international";
  category: string;
  heat_score: number;
  freshness: "rising" | "stable" | "fading";
  source_count: number;
  tags: string[];
  updated_at: string;
};

export type TimelineItem = {
  title: string;
  timestamp: string;
  source: string;
};

export type EntityItem = {
  name: string;
  entity_type: "person" | "org" | "location";
};

export type SourceItem = {
  title: string;
  publisher: string;
  publish_time: string;
  url: string;
  snippet: string;
};

export type TopicDetail = TopicSummary & {
  timeline: TimelineItem[];
  entities: EntityItem[];
  sources: SourceItem[];
};

export type PaginatedTopics = {
  items: TopicSummary[];
  total: number;
  page: number;
  size: number;
};

async function get<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
}

export const api = {
  listTopics(params?: Record<string, string>) {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return get<PaginatedTopics>(`${BASE}/topics${qs}`);
  },
  getTopicDetail(slug: string, lang?: string) {
    const qs = lang ? `?lang=${lang}` : "";
    return get<TopicDetail>(`${BASE}/topics/${encodeURIComponent(slug)}${qs}`);
  },
  search(q: string, params?: Record<string, string>) {
    const all = { q, ...params };
    return get<PaginatedTopics>(`${BASE}/search?${new URLSearchParams(all)}`);
  },
  async listSaved(lang?: string) {
    const qs = lang ? `?lang=${lang}` : "";
    return get<TopicSummary[]>(`${BASE}/saved${qs}`);
  },
  async saveTopic(topicId: string) {
    await fetch(`${BASE}/saved`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic_id: topicId }),
    });
  },
  async removeSaved(topicId: string) {
    await fetch(`${BASE}/saved/${encodeURIComponent(topicId)}`, { method: "DELETE" });
  },
};
