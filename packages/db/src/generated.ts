export type Json =
	| string
	| number
	| boolean
	| null
	| { [key: string]: Json }
	| Json[];

export interface Database {
	public: {
		Tables: {
			workflow_runs: {
				Row: {
					id: string;
					audience_id: string | null;
					location: string | null;
					status: string | null;
					started_at: string | null;
					finished_at: string | null;
					created_at: string | null;
				};
				Insert: {
					id?: string;
					audience_id?: string | null;
					location?: string | null;
					status?: string | null;
					started_at?: string | null;
					finished_at?: string | null;
					created_at?: string | null;
				};
				Update: {
					id?: string;
					audience_id?: string | null;
					location?: string | null;
					status?: string | null;
					started_at?: string | null;
					finished_at?: string | null;
					created_at?: string | null;
				};
			};
		};
		Views: {};
		Functions: {};
		Enums: {};
	};
}
