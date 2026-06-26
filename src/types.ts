src/types.ts | 50 lines
```typescript
/**
 * Abstract Data Type Generator v1.2.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility
export type Type = "integer" | "string" | "boolean" | null | undefined;

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: any; // Generic mapping to allow dynamic values in schema definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function parseSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is string => typeof val === "string") as any; // Ensure only strings are returned in schema definition to match C-style expectations
}

/**
 * Abstract Data Type Definition (Rust-like enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = {
  id: string | number;      // Identifier field
  name?: string;            // Name field (nullable in schema)
  status?: "active" | null;  // Status field with specific values mapped to types
};

// Helper to convert Rust-like struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "integer" : typeof val === "number" ? "boolean" : null)); // Mapped to C/C# style types based on presence/absence of fields
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number; // Simulating Rust enums/types via TypeScript objects in this context. 
// Note: In a real scenario with full dynamic schema support, we would use the `AlchemySchema` interface to dynamically determine field types at runtime or compile-time based on dependencies.

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number; // Simulating Rust enums/types via TypeScript objects in this context. 
// Note: In a real scenario with full dynamic schema support, we would use the `AlchemySchema` interface to dynamically determine field types at runtime or compile-time based on dependencies.

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number; // Simulating Rust enums/types via TypeScript objects in this context. 
// Note: In a real scenario with full dynamic schema support, we would use the `AlchemySchema` interface to dynamically determine field types at runtime or compile-time based on dependencies.

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number; // Simulating Rust enums/types via TypeScript objects in this context. 
// Note: In a real scenario with full dynamic schema support, we would use the `AlchemySchema` interface to dynamically determine field types at runtime or compile-time based on dependencies.

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number; // Simulating Rust enums/types via TypeScript objects in this context. 
// Note: In a real scenario with full dynamic schema support, we would use the `AlchemySchema` interface to dynamically determine field types at runtime or compile-time based on dependencies.

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number; // Simulating Rust enums/types via TypeScript objects in this context. 
// Note: In a real scenario with full dynamic schema support, we would use the `AlchemySchema` interface to dynamically determine field types at runtime or compile-time based on dependencies.

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number; // Simulating Rust enums/types via TypeScript objects in this context. 
// Note: In a real scenario with full dynamic schema support, we would use the `AlchemySchema` interface to dynamically
