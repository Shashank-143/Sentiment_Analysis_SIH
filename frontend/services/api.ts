// API services for communicating with the backend

// API base URL - consider making this configurable via environment variables
const API_BASE_URL = 'http://localhost:8000/api';

export interface SentimentResult {
  comment_id: string;
  sentiment_label: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE';
  sentiment_score: number;
  confidence_score: number;
}

export interface SummaryResult {
  summary: string;
}

export interface KeywordResult {
  keywords: string[];
}

export interface ExcelProcessingResult {
  success: boolean;
  downloadUrl?: string;
  message?: string;
}

// Sentiment Analysis API
export const analyzeSentiment = async (text: string): Promise<SentimentResult> => {
  try {
    const response = await fetch(`${API_BASE_URL}/sentiment`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        comments: [
          {
            comment_id: Date.now().toString(),
            text: text
          }
        ]
      }),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    const data = await response.json();
    return data.results[0];
  } catch (error) {
    console.error('Failed to analyze sentiment:', error);
    throw error;
  }
};

// Summary Generation API
export const generateSummary = async (text: string, maxLength: number = 130, minLength: number = 30): Promise<SummaryResult> => {
  try {
    const response = await fetch(`${API_BASE_URL}/summarise`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        max_length: maxLength,
        min_length: minLength
      }),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Failed to generate summary:', error);
    throw error;
  }
};

// Keyword Extraction API
export const extractKeywords = async (text: string, topN: number = 5): Promise<KeywordResult> => {
  try {
    const response = await fetch(`${API_BASE_URL}/keywords`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        top_n: topN
      }),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Failed to extract keywords:', error);
    throw error;
  }
};

// Word Cloud Generation API
export const getWordCloudUrl = (text: string): string => {
  return `${API_BASE_URL}/wordcloud?sentence=${encodeURIComponent(text)}`;
};

// Excel Processing API
export const processExcelFile = async (file: File): Promise<Blob> => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_BASE_URL}/process-excel`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    return await response.blob();
  } catch (error) {
    console.error('Failed to process Excel file:', error);
    throw error;
  }
};