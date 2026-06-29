src/types.ts
```typescript
import { AlchemyDatabaseType } from "./alchemy_database"; // Reuse existing type definitions for schema compatibility

// ============================================================================
// 1. Define Data Types: Implement AlphabeticalType (C#), CurrencyValue, and DecimalNumber types in a separate file or via trait definitions within this module to match existing schema assumptions.
// ============================================================================

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

/**
 * Helper to convert JSON-like data structures into TypeScript types for easier mapping and validation.
 */
export function parseJsonDataToTypes(data: Record<string, unknown>): Type[] {
  return Object.values(data)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

/**
 * Helper function for parsing nested JSON structures into a hierarchy of abstract types.
 */
export function parseJsonNestedToTypes(data: Record<string, unknown>): Type[] {
  return Object.values(data)
    .map((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

/**
 * Helper function for parsing nested JSON structures into a hierarchy of abstract types.
 */
export function parseJsonNestedToTypes(data: Record<string, unknown>): Type[] {
  return Object.values(data)
    .map((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

/**
 * Helper function for parsing nested JSON structures into a hierarchy of abstract types.
 */
export function parseJsonNestedToTypes(data: Record<string, unknown>): Type[] {
  return Object.values(data)
    .map((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

/**
 * Helper function for parsing nested JSON structures into a hierarchy of abstract types.
 */
export function parseJsonNestedToTypes(data: Record<string, unknown>): Type[] {
  return Object.values(data)
    .map
