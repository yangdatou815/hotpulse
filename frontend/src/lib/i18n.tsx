import { createContext, useContext, useState, useCallback, type ReactNode } from "react";

export type Locale = "en" | "zh";

const translations = {
  en: {
    // Nav
    "nav.home": "Home",
    "nav.explore": "Explore",
    "nav.saved": "Saved",
    // Hero
    "hero.title": "What matters today",
    "hero.subtitle": "Understand the context and evolution behind trending topics. Signal over noise.",
    // Search
    "search.placeholder": "Search topics...",
    "search.filter_placeholder": "Filter topics...",
    // Regions
    "region.all": "All Regions",
    "region.domestic": "Domestic",
    "region.international": "International",
    // Categories
    "cat.all": "All",
    "cat.politics": "Politics",
    "cat.economy": "Economy",
    "cat.technology": "Technology",
    "cat.society": "Society",
    "cat.business": "Business",
    "cat.culture": "Culture",
    // Freshness
    "freshness.rising": "↑ Rising",
    "freshness.stable": "— Stable",
    "freshness.fading": "↓ Fading",
    // Featured tags
    "tag.us_iran": "🔴 US-Iran Conflict",
    // Topic card
    "card.save": "☆ Save",
    "card.saved": "✓ Saved",
    "card.sources": "sources",
    "card.source": "source",
    // Detail page
    "detail.back": "← Back to home",
    "detail.not_found": "Topic not found",
    "detail.loading": "Loading...",
    "detail.save_topic": "☆ Save topic",
    "detail.saved_topic": "✓ Saved",
    "detail.timeline": "Timeline",
    "detail.entities": "Key Entities",
    "detail.sources": "Sources",
    // Explore page
    "explore.title": "Explore",
    "explore.subtitle": "Browse topics by category, region, and keyword.",
    "explore.no_match": "No topics match",
    "explore.no_match_hint": "Try adjusting your filters or search terms.",
    // Saved page
    "saved.title": "Saved Topics",
    "saved.subtitle": "Your bookmarked topics for later reading.",
    "saved.empty": "Nothing saved yet",
    "saved.empty_hint": "Save topics from the Home or Explore pages to find them here.",
    "saved.remove": "✕ Remove",
    // Home
    "home.no_topics": "No topics found",
    "home.no_topics_hint": "Try adjusting your filters or search keywords.",
    // Footer
    "footer.text": "HotPulse · Context over clickbait",
    // Lang toggle
    "lang.toggle": "中文",
  },
  zh: {
    "nav.home": "首页",
    "nav.explore": "探索",
    "nav.saved": "收藏",
    "hero.title": "今日要闻",
    "hero.subtitle": "深入理解热点话题的来龙去脉，聚焦真正有价值的信息。",
    "search.placeholder": "搜索话题...",
    "search.filter_placeholder": "筛选话题...",
    "region.all": "全部地区",
    "region.domestic": "国内",
    "region.international": "国际",
    "cat.all": "全部",
    "cat.politics": "政治",
    "cat.economy": "经济",
    "cat.technology": "科技",
    "cat.society": "社会",
    "cat.business": "商业",
    "cat.culture": "文化",
    "freshness.rising": "↑ 升温",
    "freshness.stable": "— 平稳",
    "freshness.fading": "↓ 降温",
    "tag.us_iran": "🔴 美伊冲突",
    "card.save": "☆ 收藏",
    "card.saved": "✓ 已收藏",
    "card.sources": "条来源",
    "card.source": "条来源",
    "detail.back": "← 返回首页",
    "detail.not_found": "话题不存在",
    "detail.loading": "加载中...",
    "detail.save_topic": "☆ 收藏话题",
    "detail.saved_topic": "✓ 已收藏",
    "detail.timeline": "时间线",
    "detail.entities": "关键实体",
    "detail.sources": "信息来源",
    "explore.title": "探索",
    "explore.subtitle": "按分类、地区和关键词浏览话题。",
    "explore.no_match": "没有匹配的话题",
    "explore.no_match_hint": "尝试调整筛选条件或搜索词。",
    "saved.title": "我的收藏",
    "saved.subtitle": "收藏的话题方便稍后阅读。",
    "saved.empty": "暂无收藏",
    "saved.empty_hint": "在首页或探索页收藏感兴趣的话题。",
    "saved.remove": "✕ 移除",
    "home.no_topics": "暂无话题",
    "home.no_topics_hint": "尝试调整筛选条件或搜索关键词。",
    "footer.text": "HotPulse · 内容胜于标题党",
    "lang.toggle": "EN",
  },
} as const;

type TranslationKey = keyof typeof translations.en;

interface I18nContextValue {
  locale: Locale;
  t: (key: TranslationKey) => string;
  toggleLocale: () => void;
}

const I18nContext = createContext<I18nContextValue>(null!);

export function I18nProvider({ children }: { children: ReactNode }) {
  const [locale, setLocale] = useState<Locale>(() => {
    const saved = localStorage.getItem("hotpulse_locale");
    return (saved === "zh" || saved === "en") ? saved : "en";
  });

  const toggleLocale = useCallback(() => {
    setLocale((prev) => {
      const next = prev === "en" ? "zh" : "en";
      localStorage.setItem("hotpulse_locale", next);
      return next;
    });
  }, []);

  const t = useCallback(
    (key: TranslationKey): string => {
      return translations[locale][key] ?? key;
    },
    [locale],
  );

  return (
    <I18nContext.Provider value={{ locale, t, toggleLocale }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n() {
  return useContext(I18nContext);
}
