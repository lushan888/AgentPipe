src/types.ts | 612 lines
```typescript
/**
 * Abstract Data Type Generator v0.7.x (Rust-based)
 * 
 * This module defines robust TypeScript types for `AlchemySchema` and a dynamic type system compatible with Rust enums/types via TS objects in this context, enabling full schema flexibility without hardcoding specific field mappings during generation.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use TypeScript-style semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility and full dynamic mapping capabilities.
export type Type = "integer" | "string" | "boolean" | null | undefined;

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: unknown; // Generic key -> value in C/C# style struct definition, allowing dynamic mapping via the type system.
}

// Helper to convert JSON-like schema definitions into abstract data types for dynamic generation using a robust fallback strategy that respects existing structure while supporting generic keys and dynamic values.
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context and extending the base `Type` definition to include more robust fallbacks.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: unknown; // Generic key -> value in C/C# style struct definition, allowing dynamic mapping via the type system.
}

// Helper to convert JSON-like schema definitions into abstract data types for dynamic generation using a robust fallback strategy that respects existing structure while supporting generic keys and dynamic values.
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context and extending the base `Type` definition to include more robust fallbacks.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: unknown; // Generic key -> value in C/C# style struct definition, allowing dynamic mapping via the type system.
}

// Helper to convert JSON-like schema definitions into abstract data types for dynamic generation using a robust fallback strategy that respects existing structure while supporting generic keys and dynamic values.
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context and extending the base `Type` definition to include more robust fallbacks.

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: unknown; // Generic key -> value in C/C# style struct definition, allowing dynamic mapping via the type system.
}

// Helper to convert JSON-like schema definitions into abstract data types for dynamic generation using a robust fallback strategy that respects existing structure while supporting generic keys and dynamic values.
export function parseSchemaToTypes(schemaMap: Record<string, unknown>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter.

/**
 * Abstract Data Type Definition (Rust
