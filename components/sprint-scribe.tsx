'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';

interface Ticket {
  name: string;
  description: string;
}

interface Epic {
  epic_name: string;
  tickets: Ticket[];
}

interface ApiResponse {
  success: boolean;
  query: string;
  implementation_plan: Epic[];
  error?: string;
}

export function SprintScribe() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ApiResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch('/api/sprint-scribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query.trim() }),
      });

      const data: ApiResponse = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        success: false,
        query: query.trim(),
        implementation_plan: [],
        error: 'Failed to generate implementation plan',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 space-y-6">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold">SprintScribe</h1>
        <p className="text-gray-600">
          Transform your statement of work into detailed implementation plans
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="query" className="block text-sm font-medium mb-2">
            Statement of Work Task
          </label>
          <Textarea
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., Set up Azure Data Factory for data pipeline processing..."
            className="min-h-[100px]"
            disabled={loading}
          />
        </div>
        
        <Button 
          type="submit" 
          disabled={loading || !query.trim()}
          className="w-full"
        >
          {loading ? 'Generating Plan...' : 'Generate Implementation Plan'}
        </Button>
      </form>

      {result && (
        <div className="space-y-4">
          {result.success ? (
            <>
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <h2 className="font-semibold text-green-800 mb-2">
                  Implementation Plan Generated
                </h2>
                <p className="text-green-700 text-sm">
                  Query: {result.query}
                </p>
              </div>

              <div className="space-y-6">
                {(result.implementation_plan || []).map((epic, epicIndex) => (
                  <div
                    key={epicIndex}
                    className="border border-gray-200 rounded-lg p-6 bg-white shadow-sm"
                  >
                    <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                      <span className="bg-blue-100 text-blue-800 text-sm px-2 py-1 rounded mr-3">
                        EPIC
                      </span>
                      {epic.epic_name}
                    </h3>
                    
                    <div className="space-y-3">
                      {epic.tickets.map((ticket, ticketIndex) => (
                        <div
                          key={ticketIndex}
                          className="border-l-4 border-blue-200 pl-4 py-2 bg-gray-50 rounded-r"
                        >
                          <h4 className="font-medium text-gray-900 mb-1">
                            {ticket.name}
                          </h4>
                          <p className="text-gray-600 text-sm">
                            {ticket.description}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <h2 className="font-semibold text-red-800 mb-2">
                Error Generating Plan
              </h2>
              <p className="text-red-700 text-sm">
                {result.error || 'An unexpected error occurred'}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
} 