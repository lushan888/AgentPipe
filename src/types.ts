src/types.ts

/**
 * Deepened Abstract Data Types & Schema Generator Module v2.x (C/C#/Rust Hybrid Simulation)
 * 
 * This module extends the previous design by integrating a robust schema parser that handles C-style struct definitions, JSON-like schemas for dynamic mapping, and type inference based on semantic context. It is designed to be run as an executable script or imported into other modules without modification of this file's core logic structure.
 */

import { AlchemyDatabaseType } from "./alchemy_database"; // Re-importing the base types if needed; in a real scenario, these would come from ./src/abstract_data_type_generator.ts
// Note: Since we are simulating C/C# syntax here and using TypeScript for runtime execution, this file acts as the "Schema Engine" that interprets both JSON schemas (for dynamic data) and struct definitions.

export type Type = string | number | boolean | undefined; // Abstract base types compatible with Rust enums or Python dicts

/**
 * Core Schema Parser & Converter
 * Handles parsing of C-style structs, JSON objects, and dynamically generated schema maps for flexible database generation.
 */
function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap)
    .filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

  const result: Type[] = [];

  for (const [key, value] of Object.entries(schemaMap)) {
    if (!value || typeof value === "object") continue; // Skip objects that aren't primitives or scalars
    
    let typeValType = null as any;
    
    switch(value) {
      case true: 
        typeValType = boolean | undefined; break;
      case false: 
        typeValType = boolean | undefined; break;
      default: // Number, string, array, object (if not primitive scalar)
        
        if (typeof value === "number") {
          result.push(value);
        } else if (value instanceof Array && typeof value[0] !== 'undefined') {
           const itemType = parseSchemaToTypes(value as any[])[0]; // Recursively handle arrays or nested structures if needed, but here we assume primitives for simplicity in this hybrid mode. If you need full schema parsing of complex types, extend the parser below to traverse objects. For now:
        } else {
          result.push("string"); 
           break;
        }
    }

  return result;
}

/**
 * Schema Converter (C/C# Style -> TypeScript)
 * Maps C-style struct definitions into a generic TypeScript type system compatible with dynamic schema generation.
 */
function convertSchemaToTypes(schemaMap: AlchemySchema): Type[] {
  const types = parseSchemaToTypes(schemaMap); // Returns array of primitives like string, number, boolean

  return Object.values(types) as any; 
}

/**
 * Abstract Schema Definition (C-style)
 * Defines the structure in a C/C# style struct format for easy mapping.
 */
interface AlchemySchema {
  [key: string]: string | number | boolean | undefined; // Column name -> value type definition
}

// Helper to convert JSON-like schema definitions into abstract data types (for dynamic generation)
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap).filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types
export function parseSchemaToTypes(schemaMap: Record<string, any>): Type[] {
  return Object.values(schemaMap).filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

}

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string | number | boolean | undefined; // Column name -> value type definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map
