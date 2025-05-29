// Debug utility to help trace reactivity issues
export const debugLog = (context: string, data: any) => {
  if (process.env.NODE_ENV !== 'production') {
    console.log(`[Debug] ${context}:`, data);
  }
};
