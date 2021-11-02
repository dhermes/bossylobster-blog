import { MigrationInterface, QueryRunner } from 'typeorm';

export class tickets1635654246652 implements MigrationInterface {
  name = 'tickets1635654246652';

  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(
      `CREATE TABLE "ticket" ("id" uuid NOT NULL, "owner" character varying NOT NULL, "description" character varying NOT NULL, "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(), "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(), "resolvedAt" TIMESTAMP WITH TIME ZONE, CONSTRAINT "PK_d9a0835407701eb86f874474b7c" PRIMARY KEY ("id"))`,
    );
    await queryRunner.query(`CREATE INDEX "IDX_4fd0fa28cf982e5252b358caa9" ON "ticket" ("owner", "updatedAt") `);
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`DROP INDEX "public"."IDX_4fd0fa28cf982e5252b358caa9"`);
    await queryRunner.query(`DROP TABLE "ticket"`);
  }
}
