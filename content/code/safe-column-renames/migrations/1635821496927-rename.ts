import { MigrationInterface, QueryRunner } from 'typeorm';

export class rename1635821496927 implements MigrationInterface {
  name = 'rename1635821496927';

  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`ALTER TABLE "ticket" RENAME COLUMN "createdAt" TO "created_at"`);
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`ALTER TABLE "ticket" RENAME COLUMN "created_at" TO "createdAt"`);
  }
}
