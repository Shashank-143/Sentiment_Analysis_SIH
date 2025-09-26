// API services for communicating with the backend

// API base URL - configurable via environment variables
export const isDevelopment = process.env.NODE_ENV === 'development';
export const DEFAULT_API_URL = isDevelopment
  ? 'http://localhost:8000/api'
  : process.env.NEXT_PUBLIC_ENV === 'staging'
    ? 'https://sih.shashankgoel.tech'
    : 'https://sentiment-analysis-sih-backend-16fbf47c4821.herokuapp.com/api';

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || DEFAULT_API_URL;

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

function timeoutSignal(ms: number): AbortSignal {
  const controller = new AbortController();
  setTimeout(() => controller.abort(), ms);
  return controller.signal;
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
    
    // Log more detailed connection information for debugging
    console.log(`Current environment: ${process.env.NODE_ENV}`);
    console.log(`Using API URL: ${API_BASE_URL}/process-excel`);
    
    // Test server connectivity before sending the file
    try {
      console.log(`Testing connectivity to ${API_BASE_URL}/status...`);
      const statusResponse = await fetch(`${API_BASE_URL}/status`, { 
        method: 'GET', 
        mode: 'cors',
        headers: { 'Content-Type': 'application/json' },
        signal: timeoutSignal(10000) // ✅ 10 second timeout
      });
      
      if (!statusResponse.ok) {
        throw new Error(`Server returned ${statusResponse.status}: ${statusResponse.statusText}`);
      }
      
      console.log('Connectivity test successful');
    } catch (connError: any) {
      console.error('Backend server connectivity test failed:', connError);
      throw new Error(`Cannot connect to server (${connError.message}). Please check your internet connection and ensure the backend server is running.`);
    }
    
    console.log(`Uploading file: ${file.name} (${file.size} bytes)`);
    const response = await fetch(`${API_BASE_URL}/process-excel`, {
      method: 'POST',
      body: formData,
      redirect: 'follow',
      mode: 'cors',
      credentials: 'include', 
      signal: timeoutSignal(600000) // ✅ 10 min timeout
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Server error response:', errorText);
      if (response.status === 400 && errorText.includes("comment_id")) {
        throw new Error('Invalid Excel format. File must contain "comment_id" and "comment" columns.');
      } else if (response.status === 400 && errorText.includes("Excel")) {
        throw new Error('Invalid Excel file format. Please check the format and try again.');
      } else {
        throw new Error(`Error ${response.status}: ${errorText || response.statusText}`);
      }
    }

    const blob = await response.blob();
    if (!blob || blob.size === 0) {
      throw new Error('Received empty response from server');
    }
    
    return blob;
  } catch (error: any) {
    // Better handle network errors
    if (error.name === 'AbortError') {
      console.error('Request timed out');
      throw new Error('Request timed out. Excel processing is taking too long. Please try with a smaller file or try again later.');
    } else if (error.message === 'Failed to fetch') {
      console.error('Network error - Failed to fetch');
      throw new Error('Network connection error. Please check your internet connection and ensure the backend server is running.');
    } else if (error.message && error.message.includes('NetworkError')) {
      console.error('CORS or network error:', error);
      throw new Error('Network error. This might be due to CORS restrictions or network connectivity issues.');
    } else {
      console.error('Failed to process Excel file:', error);
      
      // Provide more user-friendly error messages
      const errorMessage = error.message || 'Unknown error';
      if (errorMessage.includes('Excel') || errorMessage.includes('format')) {
        throw new Error(errorMessage); // Excel-specific errors are already user-friendly
      } else {
        throw new Error(`Error processing file: ${errorMessage}`);
      }
    }
  }
};