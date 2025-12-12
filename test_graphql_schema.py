"""Quick test to verify GraphQL schema loads correctly"""

try:
    from app.graphql.schema import schema
    
    print("✅ GraphQL schema loaded successfully!")
    print(f"\nSchema has {len(schema._schema.query_type.fields)} query fields")
    print(f"Schema has {len(schema._schema.mutation_type.fields)} mutation fields")
    
    print("\n📋 Available Queries:")
    for field_name in sorted(schema._schema.query_type.fields.keys()):
        print(f"  - {field_name}")
    
    print("\n🔧 Available Mutations:")
    for field_name in sorted(schema._schema.mutation_type.fields.keys()):
        print(f"  - {field_name}")
    
    print("\n✨ All GraphQL operations are ready to use!")
    
except Exception as e:
    print(f"❌ Error loading schema: {e}")
    import traceback
    traceback.print_exc()
