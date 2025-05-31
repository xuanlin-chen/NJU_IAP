// Debug utility to help trace reactivity issues
// biome-ignore lint/suspicious/noExplicitAny: <explanation>
export const debugLog = (context: string, data: any) => {
  if (process.env.NODE_ENV !== 'production') {
    console.log(`[Debug] ${context}:`, data);
  }
};
