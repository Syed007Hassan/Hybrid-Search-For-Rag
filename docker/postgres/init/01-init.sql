-- Create the vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the HNSW access method (wrapped in DO block to handle if exists)
DO $$
BEGIN
    -- Check if the access method already exists
    IF NOT EXISTS (
        SELECT 1 
        FROM pg_am 
        WHERE amname = 'hnsw'
    ) THEN
        CREATE ACCESS METHOD hnsw TYPE INDEX HANDLER hnsw_handler;
    END IF;
END
$$;

-- Set up the operator class (wrapped in DO block to handle if exists)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_opclass
        WHERE opcname = 'vector_l2_ops'
    ) THEN
        CREATE OPERATOR CLASS vector_l2_ops
        DEFAULT FOR TYPE vector USING hnsw AS
        OPERATOR 1 <-> (vector, vector) FOR ORDER BY float_ops,
        FUNCTION 1 l2_distance(vector, vector);
    END IF;
END
$$; 