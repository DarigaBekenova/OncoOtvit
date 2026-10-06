export type DemoSample = {
  id: number;
  description: string;
  features: Record<string, number>;
  reference_class: "benign" | "malignant";
};

export type Prediction = {
  id: number;
  sample_name: string;
  reference_class: string;
  predicted_class: "benign" | "malignant";
  malignant_probability: number;
  model_version: string;
  created_at: string;
  disclaimer: string;
};

export type ModelMetrics = {
  dataset: string;
  sample_count: number;
  train_fraction: number;
  metrics: Record<string, number>;
};

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? process.env.API_URL ?? "http://localhost:8000";

export async function getSamples(): Promise<DemoSample[]> {
  const response = await fetch(`${API_URL}/api/v1/predictions/samples`, { cache: "no-store" });
  if (!response.ok) throw new Error(`API error ${response.status}`);
  return response.json();
}

export async function getMetrics(): Promise<ModelMetrics> {
  const response = await fetch(`${API_URL}/api/v1/predictions/metrics`, { cache: "no-store" });
  if (!response.ok) throw new Error(`API error ${response.status}`);
  return response.json();
}

export async function createPrediction(
  features: Record<string, number>,
  sampleName: string,
  referenceClass: string,
): Promise<Prediction> {
  const params = new URLSearchParams({ sample_name: sampleName, reference_class: referenceClass });
  const response = await fetch(`${API_URL}/api/v1/predictions?${params.toString()}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ features }),
    cache: "no-store",
  });
  if (!response.ok) throw new Error(`API error ${response.status}`);
  return response.json();
}

export async function getHistory(): Promise<Prediction[]> {
  const response = await fetch(`${API_URL}/api/v1/predictions?limit=50`, { cache: "no-store" });
  if (!response.ok) throw new Error(`API error ${response.status}`);
  return response.json();
}
