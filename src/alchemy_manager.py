// src/interface.d.ts
export type doohickey_type = 'zombie' | 'whitsit';

interface ConnectInterface {
  connect: (targetId?: string, options?: Record<string, any>) => Promise<void>;
}

type DoohickeyType extends keyof typeof doohickiesMap : 'zombie' | 'whitsit' {}

// Define the standard types for common gizmos and whatsits based on context.
const doohickies = {
  zombie: (id?: string) => Promise<{ id: number; name: string }>, // Zombie ID mapping to internal index or object key if available, otherwise fallback
};

export default ConnectInterface;
